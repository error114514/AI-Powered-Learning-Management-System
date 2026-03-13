package com.controller;

import java.io.File;
import java.io.FileInputStream;
import java.util.Arrays;
import java.util.Base64;
import java.util.Map;
import java.util.Date;
import javax.servlet.http.HttpServletRequest;

import com.utils.FaceUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.util.ResourceUtils;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import com.baomidou.mybatisplus.mapper.EntityWrapper;
import com.annotation.IgnoreAuth;

import com.entity.StudentEntity;
import com.entity.view.StudentView;

import com.service.StudentService;
import com.service.TokenService;
import com.utils.PageUtils;
import com.utils.R;
import com.utils.MPUtil;

/**
 * Student
 * 后端接口
 * @author 
 * @email 
 
 */
@RestController
@RequestMapping("/student")
public class StudentController {
    @Autowired
    private StudentService studentService;


    
	@Autowired
	private TokenService tokenService;
	
	/**
	 * 登录
	 */
	@IgnoreAuth
	@RequestMapping(value = "/login")
	public R login(String username, String password, String captcha, HttpServletRequest request) {
		StudentEntity u = studentService.selectOne(new EntityWrapper<StudentEntity>().eq("account", username));
		if(u==null || !u.getPassword().equals(password)) {
			return R.error("Account or Password incorrect");
		}
		
		String token = tokenService.generateToken(u.getId(), username,"student",  "Student" );
		return R.ok().put("token", token);
	}

	
	/**
     * 注册
     */
	@IgnoreAuth
    @RequestMapping("/register")
    public R register(@RequestBody StudentEntity student){
    	//ValidatorUtils.validateEntity(student);
    	StudentEntity u = studentService.selectOne(new EntityWrapper<StudentEntity>().eq("account", student.getAccount()));
		if(u!=null) {
			return R.error("Registered user already exists");
		}
		Long uId = new Date().getTime();
		student.setId(uId);
        studentService.insert(student);
        try {
            File path = new File(ResourceUtils.getURL("classpath:static").getPath());
            if(!path.exists()) {
                path = new File("");
            }
            File upload = new File(path.getAbsolutePath(),"");
            if(!upload.exists()) {
                upload.mkdirs();
            }
            File file = new File(upload.getAbsolutePath()+"/"+student.getProfile());
            try (FileInputStream imageInFile = new FileInputStream(file)) {
                byte[] imageData = new byte[(int) file.length()];
                imageInFile.read(imageData);
                FaceUtil.registerFace(Base64.getEncoder().encodeToString(imageData), student.getId().toString());
            }

        }catch (Exception e){
            e.printStackTrace();
        }
        return R.ok();
    }

	
	/**
	 * 退出
	 */
	@RequestMapping("/logout")
	public R logout(HttpServletRequest request) {
		request.getSession().invalidate();
		return R.ok("Exit successful");
	}
	
	/**
     * 获取用户的session用户信息
     */
    @RequestMapping("/session")
    public R getCurrUser(HttpServletRequest request){
    	Long id = (Long)request.getSession().getAttribute("userId");
        StudentEntity u = studentService.selectById(id);
        return R.ok().put("data", u);
    }
    
    /**
     * Password重置
     */
    @IgnoreAuth
	@RequestMapping(value = "/resetPass")
    public R resetPass(String username, HttpServletRequest request){
    	StudentEntity u = studentService.selectOne(new EntityWrapper<StudentEntity>().eq("account", username));
    	if(u==null) {
    		return R.error("Account does not exist");
    	}
        u.setPassword("123456");
        studentService.updateById(u);
        return R.ok("Password has been reset to：123456");
    }


    /**
     * 后端List
     */
    @RequestMapping("/page")
    public R page(@RequestParam Map<String, Object> params,StudentEntity student,
		HttpServletRequest request){
        EntityWrapper<StudentEntity> ew = new EntityWrapper<StudentEntity>();

		PageUtils page = studentService.queryPage(params, MPUtil.sort(MPUtil.between(MPUtil.likeOrEq(ew, student), params), params));

        return R.ok().put("data", page);
    }
    
    /**
     * 前端List
     */
	@IgnoreAuth
    @RequestMapping("/list")
    public R list(@RequestParam Map<String, Object> params,StudentEntity student, 
		HttpServletRequest request){
        EntityWrapper<StudentEntity> ew = new EntityWrapper<StudentEntity>();

		PageUtils page = studentService.queryPage(params, MPUtil.sort(MPUtil.between(MPUtil.likeOrEq(ew, student), params), params));
        return R.ok().put("data", page);
    }

	/**
     * List
     */
    @RequestMapping("/lists")
    public R list( StudentEntity student){
       	EntityWrapper<StudentEntity> ew = new EntityWrapper<StudentEntity>();
      	ew.allEq(MPUtil.allEQMapPre( student, "student")); 
        return R.ok().put("data", studentService.selectListView(ew));
    }

	 /**
     * 查询
     */
    @RequestMapping("/query")
    public R query(StudentEntity student){
        EntityWrapper< StudentEntity> ew = new EntityWrapper< StudentEntity>();
 		ew.allEq(MPUtil.allEQMapPre( student, "student")); 
		StudentView studentView =  studentService.selectView(ew);
		return R.ok("Student query successful").put("data", studentView);
    }
	
    /**
     * 后端详情
     */
    @RequestMapping("/info/{id}")
    public R info(@PathVariable("id") Long id){
        StudentEntity student = studentService.selectById(id);
        return R.ok().put("data", student);
    }

    /**
     * 前端详情
     */
	@IgnoreAuth
    @RequestMapping("/detail/{id}")
    public R detail(@PathVariable("id") Long id){
        StudentEntity student = studentService.selectById(id);
        return R.ok().put("data", student);
    }
    



    /**
     * 后端保存
     */
    @RequestMapping("/save")
    public R save(@RequestBody StudentEntity student, HttpServletRequest request){
    	student.setId(new Date().getTime()+new Double(Math.floor(Math.random()*1000)).longValue());
    	//ValidatorUtils.validateEntity(student);
    	StudentEntity u = studentService.selectOne(new EntityWrapper<StudentEntity>().eq("account", student.getAccount()));
		if(u!=null) {
			return R.error("User already exists");
		}
		student.setId(new Date().getTime());
        studentService.insert(student);
        return R.ok();
    }
    
    /**
     * 前端保存
     */
    @RequestMapping("/add")
    public R add(@RequestBody StudentEntity student, HttpServletRequest request){
    	student.setId(new Date().getTime()+new Double(Math.floor(Math.random()*1000)).longValue());
    	//ValidatorUtils.validateEntity(student);
    	StudentEntity u = studentService.selectOne(new EntityWrapper<StudentEntity>().eq("account", student.getAccount()));
		if(u!=null) {
			return R.error("User already exists");
		}
		student.setId(new Date().getTime());
        studentService.insert(student);
        return R.ok();
    }



    /**
     * edit
     */
    @RequestMapping("/update")
    @Transactional
    public R update(@RequestBody StudentEntity student, HttpServletRequest request){
        //ValidatorUtils.validateEntity(student);
        studentService.updateById(student);//全部更新
        return R.ok();
    }


    

    /**
     * del
     */
    @RequestMapping("/delete")
    public R delete(@RequestBody Long[] ids){
        studentService.deleteBatchIds(Arrays.asList(ids));
        return R.ok();
    }
    
	









}
